import React, { Fragment, useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";

const Roles = () => {
    interface Role {
        name: string;
    }

    interface Permission {
        id: number;
        name: string;
        codename: string;
    }

    let api = useAxios();
    const [roles, setRoles] = useState<Role[]>([]);
    const [roleErrMsg, setRoleErrMsg] = useState("");
    const [permErrMsg, setPermErrMsg] = useState("");
    const [showAddRoleForm, setShowAddRoleForm] = useState(false);
    const [permissions, setPermissions] = useState<Permission[]>([]);
    const [formPermissionsList, setFormPermissionsList] = useState<string[]>(
        [],
    );

    useEffect(() => {
        getRoles();
    }, []);
    const getRoles = async () => {
        try {
            let response = await api.get(`/shop-api-v1/role`);
            if (response.status === 200) {
                setRoles(() => response.data);
                if (response.data.length < 1) {
                    setRoleErrMsg(
                        "No roles available yet. Select 'Add role' to add one.",
                    );
                } else {
                    setRoleErrMsg("");
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
                setRoleErrMsg("You are not logged in...");
                return;
            }
            if (err.response.status == 403) {
                setRoleErrMsg("You don't have permissions to see roles...");
                return;
            }
            setRoleErrMsg("Can't get roles data. Contact admin...");
        }
    };

    useEffect(() => {
        getPermissions();
    }, []);
    const getPermissions = async () => {
        try {
            let response = await api.get(`/shop-api-v1/permission`);
            if (response.status === 200) {
                console.log(response.data);
                setPermissions(() => response.data);
                if (response.data.length < 1) {
                    setPermErrMsg(
                        "No roles available yet. Select 'Add role' to add one.",
                    );
                } else {
                    setPermErrMsg("");
                }
            }
        } catch (err: any) {
            console.error(
                "During getting 'Permissions', err occurred: ",
                err.message,
                "\nMessage from server:",
                err.response?.data,
            );
            if (err.response.status == 401) {
                setPermErrMsg("You are not logged in...");
                return;
            }
            if (err.response.status == 403) {
                setPermErrMsg(
                    "You don't have permissions to see permissions...",
                );
                return;
            }
            setPermErrMsg("Can't get permissions data. Contact admin...");
        }
    };

    const handleChangeFormPermissions = (
        event: React.ChangeEvent<HTMLInputElement>,
    ) => {
        const { value, checked } = event.target;
        // console.log(value)
        if (checked) {
            setFormPermissionsList([...formPermissionsList, value]);
        } else {
            setFormPermissionsList(
                formPermissionsList.filter(
                    (permission) => permission !== value,
                ),
            );
        }
    };

    const addRole: React.FormEventHandler<HTMLFormElement> = async (event) => {
        event.preventDefault();
        const roleName = event.currentTarget.roleName.value;
        try {
            let response = await api.put(
                `/shop-api-v1/role/new/`,
                { roleName, formPermissionsList },
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
                    <label>Set permissions:</label>
                    <br />
                    {/* Listing available permissions, if exists */}
                    {permErrMsg ? (
                        <div>{permErrMsg}</div>
                    ) : (
                        <div className="grid grid-cols-2 gap-x-4 w-fit ">
                            {permissions.map((perm) => (
                                <div key={perm.id}>
                                    <input
                                        type="checkbox"
                                        id={perm.codename}
                                        name={perm.codename}
                                        value={perm.codename}
                                        onChange={handleChangeFormPermissions}
                                    />
                                    <label htmlFor={perm.codename}>
                                        {perm.name}
                                    </label>
                                </div>
                            ))}
                        </div>
                    )}
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

            {roleErrMsg ? (
                <div>{roleErrMsg}</div>
            ) : (
                <>
                    <div>Available roles:</div>
                    {roles.map((role, index) => (
                        <div key={index}>{role.name}</div>
                    ))}
                </>
            )}
            {formPermissionsList}
        </div>
    );
};

export default Roles;
