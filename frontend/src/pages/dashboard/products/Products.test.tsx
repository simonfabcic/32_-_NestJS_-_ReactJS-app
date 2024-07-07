import Products from "./Products";
import { describe, test, expect, beforeEach, afterEach } from "vitest";
import MockAdapter from "axios-mock-adapter";
import axios from "axios";
import { render, waitFor, screen, fireEvent } from "@testing-library/react";

describe("product create", () => {
    let mock: MockAdapter;

    beforeEach(() => {
        mock = new MockAdapter(axios, { onNoMatch: "throwException" });
    });

    afterEach(() => {
        mock.reset();
    });

    test("product create, check if data is in HTTP request", async () => {
        const apiUrl = "/shop-api-v1/product/create/";
        mock.onPut(apiUrl).reply(201);

        const { container: wrapper } = render(<Products />);
        expect(wrapper).toBeTruthy();

        fireEvent.click(screen.getByText(/Add product/i));
        await waitFor(() => {
            const form_label = screen.getByText(/Title:/i);
            expect(form_label).toBeTruthy();
        });

        // Fill data into form
        fireEvent.change(screen.getByLabelText(/Title/i), {
            target: { value: "Test_product_title" },
        });
        fireEvent.change(screen.getByLabelText(/Description/i), {
            target: { value: "Test_product_description" },
        });
        fireEvent.change(screen.getByLabelText(/Price/i), {
            target: { value: "22" },
        });
        fireEvent.change(screen.getByLabelText(/Image/i), {
            target: { value: "" },
        });

        // Submit form
        const form = wrapper.querySelector("form");
        form && fireEvent.submit(form);

        await waitFor(() => {
            expect(mock.history.put.length).toBe(1);

            // Create `form_data` for comparison
            const form_data = new FormData();
            form_data.append("title", "Test_product_title");
            form_data.append("description", "Test_product_description");
            form_data.append("price", "22");
            form_data.append("image", "");

            // Converting FormData to a simple object for easier comparison
            const form_data_entries = Object.fromEntries(form_data.entries());
            const sent_data_entries = Object.fromEntries(
                new URLSearchParams(mock.history.put[0].data).entries(),
            );

            expect(sent_data_entries).toEqual(form_data_entries);
        });
    });
});
