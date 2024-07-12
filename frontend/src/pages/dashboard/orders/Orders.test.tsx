import axios from "axios";
import MockAdapter from "axios-mock-adapter";
import { afterEach, beforeEach, describe, expect, test } from "vitest";
import orderData from "./orderData.json";
import { render, screen, waitFor } from "@testing-library/react";
import Orders from "./Orders";

describe("order render", () => {
    let mock: MockAdapter;

    beforeEach(() => {
        mock = new MockAdapter(axios, { onNoMatch: "throwException" });
    });

    afterEach(() => {
        mock.reset();
    });

    test("render order with one order item", async () => {
        const apiUrl = "/shop-api-v1/order";
        mock.onGet(apiUrl).reply(200, orderData.one_order);

        const wrapper = render(<Orders />);
        expect(wrapper).toBeTruthy();

        await waitFor(() => {
            const order_id = screen.getByText(/Order ID: 3/i);
            expect(order_id).toBeTruthy();
            const buyer = screen.getByText(/Buyer: Alexander Jackson/i);
            expect(buyer).toBeTruthy();
            const title = screen.getByText(/This is product title/i);
            expect(title).toBeTruthy();
            const price = screen.getByText(/566.04/i);
            expect(price).toBeTruthy();
            const quantity = screen.getByDisplayValue(/7/i);
            expect(quantity).toBeTruthy();
            const button = screen.getByText(/Remove item/i);
            expect(button).toBeTruthy();
        });
    });
});
