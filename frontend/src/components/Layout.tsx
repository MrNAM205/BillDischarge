import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import Healthcheck from './Healthcheck';
import './Layout.css';

const Layout: React.FC = () => {
    return (
        <div className="layout">
            <nav className="sidebar">
                <h2>BillDischarge Cockpit</h2>
                <ul>
                    <li><Link to="/">Project Overview</Link></li>
                    <li><Link to="/remedy-journal">Remedy Journal</Link></li>
                    <li><Link to="/endorse-pdf">Endorse PDF</Link></li>
                </ul>
                <Healthcheck />
            </nav>
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;