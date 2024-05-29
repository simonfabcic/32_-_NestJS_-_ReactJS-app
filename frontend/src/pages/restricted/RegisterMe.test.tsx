import { describe, test, expect, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";

import Register from "./RegisterMe";

describe("<RegisterMe />", () => {
    test("Loads right version of form - create new profile", () => {
        const wrapper = render(
            <MemoryRouter initialEntries={["/add-new"]}>
                <Routes>
                    {/* <Register /> */}
                    <Route path="*" element={<Register />} />
                </Routes>
            </MemoryRouter>,
        );
        expect(wrapper).toBeTruthy();

        const create_profile = screen.getByText(/Create profile/i);
        expect(create_profile.textContent).toBeTruthy();

        const create_account = screen.getByText(/Create an account/i);
        expect(create_account.textContent).toBeTruthy();
    });

    test("Loads right version of form - register", () => {
        const wrapper = render(
            <MemoryRouter initialEntries={["/register"]}>
                <Routes>
                    {/* <Register /> */}
                    <Route path="*" element={<Register />} />
                </Routes>
            </MemoryRouter>,
        );
        expect(wrapper).toBeTruthy();

        const register = screen.getByText(/register/i);
        expect(register.textContent).toBeTruthy();

        const create_account = screen.getByText(/Create an account/i);
        expect(create_account.textContent).toBeTruthy();
    });

    test("Loads right version of form - edit user", () => {
        const wrapper = render(
            <MemoryRouter initialEntries={["/dashboard/users"]}>
                <Routes>
                    {/* <Register /> */}
                    <Route path="*" element={<Register />} />
                </Routes>
            </MemoryRouter>,
        );
        expect(wrapper).toBeTruthy();

        const edit_profile = screen.getByText(/Edit profile/i);
        expect(edit_profile.textContent).toBeTruthy();

        const edit_account = screen.getByText(/Edit account/i);
        expect(edit_account.textContent).toBeTruthy();
    });

    test("Loads right version of form - edit my profile", () => {
        const wrapper = render(
            <MemoryRouter initialEntries={["/me"]}>
                <Routes>
                    {/* <Register /> */}
                    <Route path="*" element={<Register />} />
                </Routes>
            </MemoryRouter>,
        );
        expect(wrapper).toBeTruthy();

        const edit_profile = screen.getByText(/Edit profile/i);
        expect(edit_profile.textContent).toBeTruthy();

        const create_account = screen.getByText(/Edit account/i);
        expect(create_account.textContent).toBeTruthy();
    });
});

describe("<Register />", () => {
    let mock: MockAdapter;

    beforeEach(() => {
        mock = new MockAdapter(axios);
    });

    afterEach(() => {
        mock.reset();
    });

    test("Allows user to select an avatar file", async () => {
        mock.onPost().reply(204);

        const { container: wrapper } = render(
            <MemoryRouter initialEntries={["/register"]}>
                <Routes>
                    {/* <Register /> */}
                    <Route path="*" element={<Register />} />
                </Routes>
            </MemoryRouter>,
        );

        const create_account = screen.getByText(/Avatar:/i);
        expect(create_account.textContent).toBeTruthy();

        const file = new File(["avatar"], "avatar.png", { type: "image/png" });

        const input = wrapper.querySelector('input[type="file"]');
        input && fireEvent.change(input, { target: { files: [file] } });

        fireEvent.change(screen.getByLabelText(/First name:/i), {
            target: { value: "John" },
        });
        fireEvent.change(screen.getByLabelText(/Last name:/i), {
            target: { value: "Doe" },
        });
        fireEvent.change(screen.getByLabelText(/Email address:/i), {
            target: { value: "john.doe@example.com" },
        });

        const form = wrapper.querySelector("form");
        form && fireEvent.submit(form);

        await waitFor(() => {
            expect(mock.history.post.length).toBe(1);
            const formData = mock.history.post[0].data;
            expect(formData).toBeInstanceOf(FormData);
            expect(formData.get("firstName")).toBe("John");
            expect(formData.get("lastName")).toBe("Doe");
            expect(formData.get("email")).toBe("john.doe@example.com");
            expect(formData.get("avatar")).toBe(file);
        });
    });
});
