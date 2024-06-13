import React, { useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";

const Roles = () => {
    interface Role {
        name: string;
    }

    let api = useAxios();
    const [roles, setRoles] = useState<Role[]>([]);
    const [errMsg, setErrMsg] = useState("");

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
            if (err.response.status == 403) {
                setErrMsg("You don't have permissions to see roles...");
                return;
            }
            setErrMsg("Can't get roles data. Contact admin...");
        }
    };

    return (
        <>
            <div>Roles</div>

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
