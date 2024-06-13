import MockAdapter from "axios-mock-adapter";
import { render, waitFor, screen } from "@testing-library/react";
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
