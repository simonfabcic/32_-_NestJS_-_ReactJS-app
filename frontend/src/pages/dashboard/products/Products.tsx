import React, { useEffect, useState } from "react";
import useAxios from "../../utils/useAxios";
const Products = () => {
    interface Product {
        id: number;
        title: string;
        price: number;
        description: string;
        image: string;
    }

    let api = useAxios();
    const baseURL = import.meta.env.VITE_BACKEND_BASE_URL;
    const [showAddProductForm, setShowAddProductForm] = useState(false);
    const [products, setProducts] = useState<Product[]>([]);

    useEffect(() => {
        getProducts();
    }, []);
    const getProducts = async () => {
        try {
            const response = await api.get(`/shop-api-v1/product`);
            if (response.status === 200) {
                setProducts(response.data);
            }
        } catch (err) {
            console.log(err);
        }
    };

    const handleAddProduct: React.FormEventHandler<HTMLFormElement> = async (
        event,
    ) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append("title", event.currentTarget.product_title.value);
        formData.append("description", event.currentTarget.description.value);
        formData.append("price", event.currentTarget.price.value);
        if (event.currentTarget.image.files.length > 0) {
            formData.append("image", event.currentTarget.image.files[0]);
        } else {
            formData.append("image", "");
        }

        try {
            let response = await api.put(
                `${baseURL}/shop-api-v1/product/create/`,
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    },
                },
            );
            if (response.status === 201) {
                getProducts();
            } else {
                console.log(response);
            }
        } catch (error) {
            console.error("Error adding product:", error);
        }
    };

    return (
        <div>
            <div>Products</div>
            <button
                className="px-4 py-2 bg-gray-400 rounded-md"
                onClick={() => setShowAddProductForm(!showAddProductForm)}
            >
                Add product
            </button>
            {showAddProductForm && (
                <form
                    action="submit"
                    onSubmit={handleAddProduct}
                    className="flex flex-col"
                >
                    <>
                        <label htmlFor="product_title">Title:</label>
                        <input
                            type="text"
                            name="product_title"
                            id="product_title"
                            className="border rounded-md mb-3 p-2"
                            required
                        />
                    </>
                    <>
                        <label htmlFor="description">Description:</label>
                        <input
                            name="description"
                            id="description"
                            className="border rounded-md mb-3 p-2"
                        ></input>
                    </>
                    <>
                        <label htmlFor="price">Price:</label>
                        <input
                            type="number"
                            name="price"
                            id="price"
                            className="border rounded-md mb-3 p-2"
                            step="0.01"
                            min="0"
                            max="1000000"
                            required
                        />
                    </>
                    <>
                        <label htmlFor="image">Image:</label>
                        <input
                            type="file"
                            name="image"
                            id="image"
                            accept="image/png, image/jpeg"
                            className="border rounded-md mb-3 p-2"
                        />
                    </>
                    <button
                        className="px-4 py-2 bg-gray-400 rounded-md"
                        type="submit"
                    >
                        Add product
                    </button>
                </form>
            )}
            <table>
                <thead>
                    <tr>
                        <th>No.</th>
                        <th>Image</th>
                        <th>Title</th>
                        <th>Price</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map((product, index) => (
                        <tr key={product.id}>
                            <td>{index + 1}</td>
                            <td>
                                {product.image === null ? (
                                    "/"
                                ) : (
                                    <img
                                        src={baseURL + product.image}
                                        className="h-8 rounded-lg block mx-auto"
                                        alt="product_image"
                                    />
                                )}
                            </td>
                            <td>{product.title}</td>
                            <td>{product.price}</td>
                            <td>{product.description}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default Products;
