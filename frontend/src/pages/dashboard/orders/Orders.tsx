import React, { useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";

const Orders = () => {
    interface Product {
        id: number;
        image: string | null;
        title: string;
        description: string;
        price: string;
    }

    interface OrderItem {
        id: number;
        order: number;
        product: Product;
        quantity: number;
    }

    interface Buyer {
        id: number;
        email: string;
        full_name: string;
        first_name: string;
        last_name: string;
        username: string;
        avatar: string | null;
        groups: string[];
    }

    interface Order {
        id: number;
        order_items: OrderItem[];
        buyer: Buyer;
    }

    let api = useAxios();
    const [orders, setOrders] = useState<Order[]>([]);

    useEffect(() => {
        getProducts();
    }, []);
    const getProducts = async () => {
        try {
            const response = await api.get(`/shop-api-v1/order`);
            if (response.status === 200) {
                setOrders(response.data);
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
            {orders.map((order) => (
                <div key={order.id} className="border rounded-lg my-3 p-2">
                    <div>Order ID: {order.id}</div>
                    <div>Buyer: {order.buyer.full_name}</div>
                    {order.order_items.map((order_item) => (
                        <div
                            key={order_item.id}
                            className="border rounded-lg m-3 p-2"
                        >
                            <div>Product ID: {order_item.product.id}</div>
                            <div>Product title: {order_item.product.title}</div>
                            <div>Product price: {order_item.product.price}</div>
                        </div>
                    ))}
                </div>
            ))}
        </>
    );
};

export default Orders;
