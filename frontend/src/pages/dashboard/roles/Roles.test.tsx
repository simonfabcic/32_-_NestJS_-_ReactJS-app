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

describe("axios mocking test", () => {
    test("should render loading followed by roles", async () => {
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
});
