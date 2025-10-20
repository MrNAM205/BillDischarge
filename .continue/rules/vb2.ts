import { Rule } from "continue";

export const rule: Rule = {
  name: "vb2",
  description: "Omni2 cognition logic: model selection, contradiction detection, and remedy scaffolding",

  async run({ task, context }) {
    const taskType = classifyTask(task);

    const selectedModel = selectModel(taskType);

    const narration = narrateDecision(taskType, selectedModel);

    return {
      model: selectedModel,
      thoughts: narration,
    };
  },
};

// 🧠 Task classifier
const taskMappings: { [key: string]: string[] } = {
  remedy: ["remedy", "ucc", "discharge"],
  contradiction: ["contradiction", "conflict", "semantic drift"],
  identity: ["identity", "sovereign", "status"],
  chat: ["summarize", "chat", "overview"],
};

function classifyTask(task: string): string {
  const lower = task.toLowerCase();
  for (const taskType in taskMappings) {
    if (taskMappings[taskType].some(keyword => lower.includes(keyword))) {
      return taskType;
    }
  }
  return "default";
}

// 🔁 Model selector
function selectModel(taskType: string): string {
  switch (taskType) {
    case "remedy":
    case "contradiction":
    case "identity":
      return "local-autodetect"; // Sovereign cognition
    case "chat":
      return "gemini-pro"; // Institutional overview
    default:
      return "gemini-flash"; // Fallback
  }
}

// 📜 Narration logic
function narrateDecision(taskType: string, model: string): string {
  return `Task classified as '${taskType}'. Using '${model}' for optimal cognition. Sovereign logic scaffolded.`;
}
