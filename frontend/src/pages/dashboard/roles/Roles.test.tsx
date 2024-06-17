import MockAdapter from "axios-mock-adapter";
import { render, waitFor, screen, fireEvent } from "@testing-library/react";
import { describe, test, expect } from "vitest";
import axios from "axios";

import Roles from "./Roles";

const mock = new MockAdapter(axios, { onNoMatch: "throwException" });

const roles = [
    { name: "Administrator" },
    { name: "User" },
    { name: "Manager" },
];

describe("rendering roles", () => {
    test("render roles, success, should render loaded roles", async () => {
        mock.onGet("/shop-api-v1/role").reply(200, roles);

        const wrapper = render(<Roles />);
        expect(wrapper).toBeTruthy();

        await waitFor(() => {
            roles.forEach((role) => {
                const text = screen.getByText(role.name);
                expect(text.textContent).toBeTruthy();
            });
        });
    });

    test("render roles, success, no roles", async () => {
        mock.onGet("/shop-api-v1/role").reply(200, []);

        const wrapper = render(<Roles />);
        expect(wrapper).toBeTruthy();

        await waitFor(() => {
            const no_roles_msg = screen.getByText(
                /No roles available yet. Select 'Add role' to add one./i,
            );
            expect(no_roles_msg).toBeTruthy();
        });
    });

    test("render roles, failure, not authenticated", async () => {
        mock.onGet("/shop-api-v1/role").reply(401);

        const wrapper = render(<Roles />);
        expect(wrapper).toBeTruthy();

        await waitFor(() => {
            const no_roles_msg = screen.getByText(/You are not logged in.../i);
            expect(no_roles_msg).toBeTruthy();
        });
    });

    test("render roles, failure, no permissions", async () => {
        mock.onGet("/shop-api-v1/role").reply(403);

        const wrapper = render(<Roles />);
        expect(wrapper).toBeTruthy();

        await waitFor(() => {
            const no_roles_msg = screen.getByText(
                /You don't have permissions to see roles.../i,
            );
            expect(no_roles_msg).toBeTruthy();
        });
    });
});

describe("rendering roles", async () => {
    test("saving role, success, should save role and re-render list of roles", async () => {
        mock.onPut("/shop-api-v1/role/new/").reply(201);
        mock.onGet("/shop-api-v1/role").reply(200, [
            { name: "Test_role_name" },
        ]);

        const { container: wrapper } = render(<Roles />);
        expect(wrapper).toBeTruthy();

        // check if form is shown
        fireEvent.click(screen.getByText(/Add role/i));
        await waitFor(() => {
            const form_label = screen.getByText(/Role name:/i);
            expect(form_label).toBeTruthy();
        });

        // filling data into form
        fireEvent.change(screen.getByLabelText(/Role name:/i), {
            target: { value: "Test_role_name" },
        });
        // submit form
        const form = wrapper.querySelector("form");
        form && fireEvent.submit(form);

        // check if submitted data sended
        await waitFor(() => {
            expect(mock.history.put.length).toBe(1);
            const putData = JSON.parse(mock.history.put[0].data); // Parse the JSON string
            expect(putData.name).toBe("Test_role_name");
        });

        // check if re-rendering new role name
        await waitFor(() => {
            const create_profile = screen.getByText(/Test_role_name/i);
            expect(create_profile.textContent).toBeTruthy();
        });
    });
});
// CONTINUE
describe("permissions in 'add role' form", async () => {
    test("check, if permissions are rendered", async () => {});
    test("check, if permissions are present in PUT request", async () => {});
});
