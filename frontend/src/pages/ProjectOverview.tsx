
import React, { useEffect, useState } from 'react';

const ProjectOverview: React.FC = () => {
    const [overview, setOverview] = useState({ goals: '', pain_points: '', agent_ancestry: '' });
    const [isEditing, setIsEditing] = useState(false);

    useEffect(() => {
        fetch('http://localhost:8000/api/project_overview')
            .then(response => response.json())
            .then(data => setOverview(data));
    }, []);

    const handleUpdate = () => {
        fetch('http://localhost:8000/api/project_overview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(overview),
        })
            .then(response => response.json())
            .then(data => {
                setOverview(data);
                setIsEditing(false);
            });
    };

    return (
        <div>
            <h2>Project Overview</h2>
            {isEditing ? (
                <div>
                    <label>Goals:</label>
                    <textarea value={overview.goals} onChange={e => setOverview({ ...overview, goals: e.target.value })} />
                    <label>Pain Points:</label>
                    <textarea value={overview.pain_points} onChange={e => setOverview({ ...overview, pain_points: e.target.value })} />
                    <label>Agent Ancestry:</label>
                    <textarea value={overview.agent_ancestry} onChange={e => setOverview({ ...overview, agent_ancestry: e.target.value })} />
                    <button onClick={handleUpdate}>Save</button>
                </div>
            ) : (
                <div>
                    <h3>Goals</h3>
                    <p>{overview.goals}</p>
                    <h3>Pain Points</h3>
                    <p>{overview.pain_points}</p>
                    <h3>Agent Ancestry</h3>
                    <p>{overview.agent_ancestry}</p>
                    <button onClick={() => setIsEditing(true)}>Edit</button>
                </div>
            )}
        </div>
    );
};

export default ProjectOverview;
