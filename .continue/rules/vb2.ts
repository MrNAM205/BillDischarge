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
function classifyTask(task: string): string {
  const lower = task.toLowerCase();

  if (lower.includes("remedy") || lower.includes("ucc") || lower.includes("discharge")) {
    return "remedy";
  }

  if (lower.includes("contradiction") || lower.includes("conflict") || lower.includes("semantic drift")) {
    return "contradiction";
  }

  if (lower.includes("identity") || lower.includes("sovereign") || lower.includes("status")) {
    return "identity";
  }

  if (lower.includes("summarize") || lower.includes("chat") || lower.includes("overview")) {
    return "chat";
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
