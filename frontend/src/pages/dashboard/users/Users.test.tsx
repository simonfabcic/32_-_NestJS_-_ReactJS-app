import { describe, test, expect, beforeEach, afterEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import MockAdapter from "axios-mock-adapter";
import axios from "axios";
import tableData from "./tableData.json";

import Users from "./Users";

let mock: MockAdapter;

beforeEach(() => {
    mock = new MockAdapter(axios, { onNoMatch: "throwException" });
});

afterEach(() => {
    mock.reset();
    mock.restore();
});

describe("<App />", () => {
    let data = tableData.no_profiles;
    test("App mounts properly, shows no data", async () => {
        mock.onGet().reply(200, data);

        const wrapper = render(
            <Router>
                <Users />
            </Router>,
        );
        expect(wrapper).toBeTruthy();

        const text = screen.getByText(/Users/i);
        expect(text.textContent).toBeTruthy();

        const b1 = wrapper.container.querySelector("button");
        expect(b1?.textContent).toBe("Add User");

        await waitFor(() => {
            const no_profiles = screen.getByText(
                /Didn't receive any profiles. Nothing to show./i,
            );
            expect(no_profiles.textContent).toBeTruthy;
        });
    });

    test("User avatar load properly", async () => {
        let data = tableData.six_profiles;
        mock.onGet().reply(200, data);

        const wrapper = render(
            <Router>
                <Users />
            </Router>,
        );
        expect(wrapper).toBeTruthy();

        await waitFor(() => {
            data.rows.forEach((row) => {
                if (row.avatar === null) {
                    const tdElements = screen.getAllByText("/");
                    expect(tdElements).toHaveLength(5);
                } else {
                    const text = screen.getAllByAltText("avatar");
                    expect(text).toBeTruthy();
                }
            });
        });
    });
});
