import React, { useEffect, useState } from "react";

interface ProjectData {
  summary: string;
  goals: string[];
  pain_points: string[];
  agent_lineage: string;
}

const ProjectOverview: React.FC = () => {
  const [data, setData] = useState<ProjectData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/project")
      .then((res) => res.json())
      .then((json) => {
        setData(json);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Failed to fetch project overview:", err);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading project overview…</div>;
  if (!data) return <div>Unable to load project overview.</div>;

  return (
    <div className="project-overview">
      <h2>🧠 Project Overview</h2>
      <p><strong>Summary:</strong> {data.summary}</p>

      <h3>🎯 Goals</h3>
      <ul>
        {data.goals.map((goal, idx) => (
          <li key={idx}>{goal}</li>
        ))}
      </ul>

      <h3>⚠️ Pain Points</h3>
      <ul>
        {data.pain_points.map((point, idx) => (
          <li key={idx}>{point}</li>
        ))}
      </ul>

      <h3>🧬 Agent Lineage</h3>
      <p>{data.agent_lineage}</p>
    </div>
  );
};

export default ProjectOverview;