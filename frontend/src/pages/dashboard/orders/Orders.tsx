import React, { useEffect } from "react";
import useAxios from "../../utils/useAxios";

const Orders = () => {
    interface Order {
        id: number;
    }

    let api = useAxios();

    useEffect(() => {
        getProducts();
    }, []);
    const getProducts = async () => {
        try {
            const response = await api.get(`/shop-api-v1/order`);
            if (response.status === 200) {
                console.log(response.data);
            }
        } catch (err) {
            console.log(err);
        }
    };

    return (
        <>
            <div>Orders</div>
            {/* TODO: table of orders */}
            {/* TODO: export to csv */}
        </>
    );
};

export default Orders;
