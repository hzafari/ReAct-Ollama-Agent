import re, json
from tools import TOOLS
import os
import time

def safe_parse_json(output: str):
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except json.JSONDecodeError:
        return None



SYSTEM_PROMPT = """
You are a reasoning agent. ALWAYS respond with a SINGLE JSON object.
JSON structure:
{
  "thought": "your reasoning",
  "action": "file_search" | "file_reader" | "calculator" | "final",
  "action_input": "keyword, filename, or answer"
}

Rules:
1. To find info, use 'file_search' with a keyword.
2. Use 'file_reader' ONLY with filenames returned by 'file_search'.
3. If the answer is in FACTS EXTRACTED, use action 'final' immediately.
4. If a tool returns a filename, DO NOT call that same tool again. 
5. Immediately use 'file_reader' with the filename you just discovered.
6. If you already have the answer in the 'Observation', use the 'final' action.
7. NEVER perform the same 'action' with the same 'action_input' twice in a row. 
8. If 'file_search' gives you a filename, your NEXT action MUST be 'file_reader'.
9. Do not re-search for a file you have already found.

10. CRITICAL FINAL STEP:
When you use action: "final", you MUST write the complete answer in the "action_input" field. 
Example:
{
  "thought": "I have found the starting date of the plan in schedule.txt.",
  "action": "final",
  "action_input": "The starting date in Feb 2, 2022."
}
"""

def build_prompt(user_input, scratchpad, memory, knowledge_base):
    # Only show the very last discovery to keep the prompt focused
    kb_content = knowledge_base[-1] if knowledge_base else "No facts discovered yet."
    
    return f"""{SYSTEM_PROMPT}

    FACTS DISCOVERED:
    {kb_content}

    CURRENT TASK REASONING:
    {scratchpad[-500:]} # Only show the last 500 characters of reasoning to prevent bloat

    User Question: {user_input}"""



class ReActAgent:
    def __init__(self, llm, max_steps=8):
        self.llm = llm
        self.max_steps = max_steps
        self.memory = []
        self.knowledge_base = [] # Permanent store for raw facts
        self.current_trace = []

    def run(self, question):
        scratchpad = ""
        self.current_trace = [] 
        
        for step in range(self.max_steps):
            print(f"===================== step: {step} =================\n")
            prompt = build_prompt(question, scratchpad, self.memory, self.knowledge_base)
            output = self.llm.generate(prompt)
            response = safe_parse_json(output)

            if not response:
                scratchpad += "\nObservation: Invalid JSON format. Please output ONLY JSON."
                continue

            thought = response.get("thought")
            action = response.get("action")
            action_input = response.get("action_input")

            # --- PREPARE TRACE ENTRY ---
            step_entry = {
                "step": step,
                "thought": thought,
                "action": action,
                "action_input": action_input,
                "observation": None
            }

            if action == "final":
                step_entry["observation"] = "Task Complete"
                self.current_trace.append(step_entry) # RECORD THE FINAL STEP
                self.memory.append({"question": question, "answer": action_input})
                self.export_trace_to_markdown() # EXPORT NOW
                #return action_input

                answer = action_input
    
                if not answer or answer == "None" or answer == "":
                    answer = "I found the information, but failed to format the final string. Please check the trace."

                print(f"FINAL ANSWER: {answer}")
                
                # 3. Crucial: Return the answer to exit the while loop
                return answer

            if action in TOOLS:
                observation = TOOLS[action].run(action_input)
                
                # Update knowledge base
                fact = f"Result of {action}({action_input}): {observation}"
                if fact not in self.knowledge_base:
                    self.knowledge_base.append(fact)

                # RECORD THE STEP FOR TRACE
                step_entry["observation"] = observation
                self.current_trace.append(step_entry)

                new_step = f"\nThought: {thought}\nAction: {action}\nInput: {action_input}\nObservation: {observation}"

                # LOOP BUSTER: If this exact action/input is already in the scratchpad, 
                # don't add the full text again. Add a warning instead.
                if f"Action: {action}" in scratchpad and f"Input: {action_input}" in scratchpad:
                    scratchpad += f"\nNote: I already tried {action} with {action_input}. I must try something else."
                else:
                    scratchpad += new_step

                # Update scratchpad
                #scratchpad += f"\nThought: {thought}\nAction: {action}\nInput: {action_input}\nObservation: {observation}"
            else:
                scratchpad += f"\nObservation: Tool '{action}' not found."
            print(f"----------- scratchpad -----------\n")
            print(scratchpad)

        self.export_trace_to_markdown()
        return "Max steps reached."
    

    def export_trace_to_markdown(self):

        
        if not os.path.exists("traces"):
            os.makedirs("traces")
            
        filename = f"traces/trace_{int(time.time())}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# 🕵️ Agent Reasoning Trace\n\n")
            for entry in self.current_trace:
                f.write(f"### Step {entry['step']}\n")
                f.write(f"**Thought:** {entry['thought']}\n\n")
                f.write(f"**Action:** `{entry['action']}`\n")
                f.write(f"**Input:** `{entry['action_input']}`\n\n")
                f.write(f"**Observation:**\n```text\n{entry['observation']}\n```\n\n")
                f.write("---\n")
        print(f"Successfully exported trace to {filename}")