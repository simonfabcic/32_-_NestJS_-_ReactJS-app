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
            let response = await api.get(`/shop-api-v1/roles`);
            if (response.status === 200) {
                setRoles(() => response.data);
                if (response.data.length < 1)
                    setErrMsg(
                        "No roles available yet. Select 'Add role' to add one.",
                    );
            }
        } catch (err: any) {
            console.error(
                "During getting 'Roles', err occurred: ",
                err.message,
                "\nMessage from server:",
                err.response?.data,
            );
            console.log(err.response.status);
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
                    "During creating/editing 'Profile', err occurred: ",
                    err.message,
                );
            }
        }
    };

    return (
        <>
            <div>Roles</div>

            <button
                className="px-4 py-2 bg-gray-400 rounded-md"
                onClick={() => setShowAddRoleForm(!showAddRoleForm)}
            >
                Add Role
            </button>

            {showAddRoleForm && (
                <form action="submit" onSubmit={addRole}>
                    <label htmlFor="roleName">Role Name:</label>
                    <input type="text" id="roleName" name="roleName" />
                    <br />
                    <label>Set permissions:</label>
                    <br />
                    <input
                        type="checkbox"
                        id="perm1"
                        name="perm1"
                        value="Bike"
                    />
                    <label htmlFor="perm1"> Can edit roles</label>
                    <br />
                    <input
                        type="checkbox"
                        id="perm2"
                        name="perm2"
                        value="Car"
                    />
                    <label htmlFor="perm2"> can view roles</label>
                    <br />
                    <input
                        type="checkbox"
                        id="perm3"
                        name="vehicle3"
                        value="Boat"
                    />
                    <label htmlFor="vehicle3"> can view users</label>
                    <button type="submit">Save role</button>
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
        </>
    );
};

export default Roles;
