import React, { useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";

const Roles = () => {
    interface Role {
        name: string;
    }

    let api = useAxios();
    const [roles, setRoles] = useState<Role[]>([]);
    const [errMsg, setErrMsg] = useState("");
    const [showAddRoleForm, setShowAddRoleForm] = useState(false);

    useEffect(() => {
        getRoles();
    }, []);
    const getRoles = async () => {
        try {
            let response = await api.get(`/shop-api-v1/role`);
            if (response.status === 200) {
                setRoles(() => response.data);
                if (response.data.length < 1) {
                    setErrMsg(
                        "No roles available yet. Select 'Add role' to add one.",
                    );
                } else {
                    setErrMsg("");
                }
            }
        } catch (err: any) {
            console.error(
                "During getting 'Roles', err occurred: ",
                err.message,
                "\nMessage from server:",
                err.response?.data,
            );
            if (err.response.status == 401) {
                setErrMsg("You are not logged in...");
                return;
            }
            if (err.response.status == 403) {
                setErrMsg("You don't have permissions to see roles...");
                return;
            }
            setErrMsg("Can't get roles data. Contact admin...");
        }
    };

    const addRole: React.FormEventHandler<HTMLFormElement> = async (event) => {
        event.preventDefault();
        const name = event.currentTarget.roleName.value;

        try {
            let response = await api.put(
                `/shop-api-v1/role/new/`,
                { name },
                {
                    headers: {
                        "Content-Type": "application/json",
                    },
                },
            );
            if (response.status === 201) {
                getRoles();
            }
        } catch (err) {
            if (err instanceof Error) {
                console.error(
                    "During creating/editing 'Role', err occurred: ",
                    err.message,
                );
            }
        }
    };

    return (
        <div>
            <div>Roles</div>

            <button
                className="px-4 py-2 bg-gray-400 rounded-md"
                onClick={() => setShowAddRoleForm(!showAddRoleForm)}
            >
                Add role
            </button>

            {showAddRoleForm && (
                <form action="submit" onSubmit={addRole}>
                    <label htmlFor="roleName">Role name:</label>
                    <br />
                    <input
                        className="border rounded-md mb-3 pl-2"
                        type="text"
                        id="roleName"
                        name="roleName"
                    />
                    <br />

                    <button
                        className="px-4 py-2 bg-gray-400 rounded-md mb-3"
                        type="submit"
                    >
                        Save role
                    </button>
                    <hr />
                </form>
            )}

            {errMsg ? (
                <div>{errMsg}</div>
            ) : (
                <>
                    <div>Available roles:</div>
                    {roles.map((role, index) => (
                        <div key={index}>{role.name}</div>
                    ))}
                </>
            )}
        </div>
    );
};

export default Roles;
