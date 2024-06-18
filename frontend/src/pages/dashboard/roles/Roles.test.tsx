import MockAdapter from "axios-mock-adapter";
import { render, waitFor, screen, fireEvent } from "@testing-library/react";
import { describe, test, expect, beforeEach, afterEach } from "vitest";
import axios from "axios";

import Roles from "./Roles";

// const mock = new MockAdapter(axios, { onNoMatch: "throwException" });

const roles = [
    { name: "Administrator" },
    { name: "User" },
    { name: "Manager" },
];

const permissions = [
    { id: 1, name: "Permission 1", codename: "perm_1" },
    { id: 2, name: "Permission 2", codename: "perm_2" },
];

describe("rendering roles", () => {
    let mock: MockAdapter;

    beforeEach(() => {
        mock = new MockAdapter(axios, { onNoMatch: "throwException" });
    });

    afterEach(() => {
        mock.reset();
    });

    test("render roles, success, should render loaded roles", async () => {
        mock.onGet("/shop-api-v1/role").reply(200, roles);
        mock.onGet("/shop-api-v1/permission").reply(200, permissions);

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
        mock.onGet("/shop-api-v1/permission").reply(200, permissions);

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
        mock.onGet("/shop-api-v1/permission").reply(200, permissions);

        const wrapper = render(<Roles />);
        expect(wrapper).toBeTruthy();

        await waitFor(() => {
            const no_roles_msg = screen.getByText(/You are not logged in.../i);
            expect(no_roles_msg).toBeTruthy();
        });
    });

    test("render roles, failure, no permissions", async () => {
        mock.onGet("/shop-api-v1/role").reply(403);
        mock.onGet("/shop-api-v1/permission").reply(200, permissions);

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

describe("rendering roles", () => {
    let mock: MockAdapter;

    beforeEach(() => {
        mock = new MockAdapter(axios, { onNoMatch: "throwException" });
    });

    afterEach(() => {
        mock.reset();
    });

    test.skip("saving role, success, should save role and re-render list of roles", async () => {
        // Mock the PUT request to add a new role
        mock.onPut("/shop-api-v1/role/new/").reply(201);

        // Mock the GET request to retrieve roles
        mock.onGet("/shop-api-v1/role").reply(200, [
            { name: "Test_role_name" },
        ]);

        // Mock the GET request to retrieve permissions
        mock.onGet("/shop-api-v1/permission").reply(200, permissions);

        const { container: wrapper } = render(<Roles />);
        expect(wrapper).toBeTruthy();

        // Check if form is shown
        fireEvent.click(screen.getByText(/Add role/i));
        await waitFor(() => {
            const form_label = screen.getByText(/Role name:/i);
            expect(form_label).toBeTruthy();
        });

        // Fill data into form
        fireEvent.change(screen.getByLabelText(/Role name:/i), {
            target: { value: "Test_role_name" },
        });

        // Submit form
        const form = wrapper.querySelector("form");
        form && fireEvent.submit(form);

        // Check if submitted data sent
        await waitFor(() => {
            expect(mock.history.put.length).toBe(1);
            const putData = JSON.parse(mock.history.put[0].data); // Parse the JSON string
            expect(putData.roleName).toBe("Test_role_name");
        });

        // Check if re-rendering new role name
        await waitFor(() => {
            const create_profile = screen.getByText(/Test_role_name/i);
            expect(create_profile.textContent).toBeTruthy();
        });
    });
});

describe("permissions in 'add role' form", async () => {
    let mock: MockAdapter;

    beforeEach(() => {
        mock = new MockAdapter(axios, { onNoMatch: "throwException" });
    });

    afterEach(() => {
        mock.reset();
    });

    test("check, if permissions are rendered", async () => {
        mock.onGet("/shop-api-v1/role").reply(200, [
            { name: "Test_role_name" },
        ]);
        mock.onGet("/shop-api-v1/permission").reply(200, permissions);

        const { container: wrapper } = render(<Roles />);
        expect(wrapper).toBeTruthy();

        // Check if form is shown
        fireEvent.click(screen.getByText(/Add role/i));
        await waitFor(() => {
            const form_label = screen.getByText(/Role name:/i);
            expect(form_label).toBeTruthy();
            const perm_1 = screen.getByText(/Permission 1/i);
            expect(perm_1).toBeTruthy();
            const perm_2 = screen.getByText(/Permission 2/i);
            expect(perm_2).toBeTruthy();
        });
    });

    test("check, if permissions are present in PUT request", async () => {
        mock.onGet("/shop-api-v1/role").reply(200, [
            { name: "Test_role_name" },
        ]);
        mock.onGet("/shop-api-v1/permission").reply(200, permissions);
        mock.onPut("/shop-api-v1/role/new/").reply(201);

        const { container: wrapper } = render(<Roles />);
        expect(wrapper).toBeTruthy();

        // Check if form is shown
        fireEvent.click(screen.getByText(/Add role/i));
        await waitFor(() => {
            const form_label = screen.getByText(/Role name:/i);
            expect(form_label).toBeTruthy();
            const perm_1 = screen.getByText(/Permission 1/i);
            expect(perm_1).toBeTruthy();
            const perm_2 = screen.getByText(/Permission 2/i);
            expect(perm_2).toBeTruthy();
        });

        // Fill data into form
        fireEvent.change(screen.getByLabelText(/Role name:/i), {
            target: { value: "Test_role_name" },
        });
        // CONTINUE
        // fireEvent.click(screen.getByLabelText(/Permission 1/i));

        // Submit form
        const form = wrapper.querySelector("form");
        form && fireEvent.submit(form);

        // Check if submitted data sent
        await waitFor(() => {
            expect(mock.history.put.length).toBe(1);
            const putData = JSON.parse(mock.history.put[0].data); // Parse the JSON string
            console.log("putData: ", putData);
            expect(putData.roleName).toBe("Test_role_name");
            // expect(putData.formPermissionsList[0]).toBe("perm_1");
        });
    });
});
