import { useEffect, useMemo, useState } from "react";
import "./AdminDashboard.css";
import { API_URL } from "../config";



export default function AdminDashboard() {

    const [users, setUsers] = useState([]);
    const [search, setSearch] = useState("");

    async function loadUsers() {

        const token = localStorage.getItem("token");

        const res = await fetch(
            `${API_URL}/admin/users`,
            {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        const data = await res.json();

        setUsers(data);

    }

    useEffect(() => {

        loadUsers();

    }, []);

    const filtered = useMemo(() => {

        return users.filter(user =>

            user.username
                .toLowerCase()
                .includes(search.toLowerCase())

            ||

            user.email
                .toLowerCase()
                .includes(search.toLowerCase())

        );

    }, [users, search]);

    return (

        <div className="admin-dashboard">

            <h1>🛡 Admin Dashboard</h1>

            <div className="admin-cards">

                <div className="stat-card">

                    <h3>Total Users</h3>

                    <span>{users.length}</span>

                </div>

                <div className="stat-card">

                    <h3>Premium</h3>

                    <span>

                        {users.filter(u => u.is_premium).length}

                    </span>

                </div>

                <div className="stat-card">

                    <h3>Banned</h3>

                    <span>

                        {users.filter(u => u.is_banned).length}

                    </span>

                </div>

                <div className="stat-card">

                    <h3>Active</h3>

                    <span>

                        {users.filter(u => !u.is_banned).length}

                    </span>

                </div>

            </div>

            <input

                placeholder="🔍 Search username or email..."

                value={search}

                onChange={(e) => setSearch(e.target.value)}

            />

            <div className="table-wrapper">

                <table className="admin-table">

                    <thead>

                        <tr>

                            <th>ID</th>

                            <th>Username</th>

                            <th>Email</th>

                            <th>Premium</th>

                            <th>Status</th>

                        </tr>

                    </thead>

                    <tbody>

                        {

                            filtered.map(user => (

                                <tr key={user.id}>

                                    <td>{user.id}</td>

                                    <td>{user.username}</td>

                                    <td>{user.email}</td>

                                    <td>

                                        {

                                            user.is_premium

                                                ?

                                                "⭐ Premium"

                                                :

                                                "Free"

                                        }

                                    </td>

                                    <td>

                                        {

                                            user.is_banned

                                                ?

                                                "🚫 Banned"

                                                :

                                                "🟢 Active"

                                        }

                                    </td>

                                </tr>

                            ))

                        }

                    </tbody>

                </table>

            </div>

        </div>

    );

}