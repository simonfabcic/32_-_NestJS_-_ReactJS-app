import React, { useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";

const Roles = () => {
    // INTERFACES ---------------------------------------------------------------
    // --------------------------------------------------------------------------
    interface Role {
        name: string;
    }

    // VARIABLES ----------------------------------------------------------------
    // --------------------------------------------------------------------------
    const [roles, setRoles] = useState<Role[]>([]);
    let api = useAxios();
    let status = "";

    // API REQUESTS -------------------------------------------------------------
    // --------------------------------------------------------------------------

    useEffect(() => {
        getProfiles();
    }, []);
    let getProfiles = async () => {
        try {
            let response = await api.get(`/shop-api-v1/roles`);
            if (response.status === 200) {
                setRoles(() => response.data);
                if (response.data.rows.length < 1)
                    status = "Didn't receive any roles. Nothing to show.";
            }
        } catch (err: any) {
            console.error(
                "During getting 'Roles', err occurred: ",
                err.message,
                "\nMessage from server:",
                err.response?.data
            );
            status = "Can't get roles data. Contact admin...";
        }
    };

    return (
        <>
            <div>Roles</div>
            {roles && <div>Test</div>}
            {roles &&
                roles.map((role, index) => <div key={index}>{role.name}</div>)}
        </>
    );
};

export default Roles;
