import { describe, test, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import MockAdapter from "axios-mock-adapter";
import axios from "axios";
import tableData from "./tableData.json"

import Users from "./Users";

const mock = new MockAdapter(axios, { onNoMatch: "throwException" });

describe("<App />", () => {
  test("App mounts properly", () => {
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
  });

  test("App mounts properly", async () => {
    let url = `/shop-api-v1/profiles?offset=0&page=1&page_size=100&sort_by=role&sort_order=ASC`
    mock.onGet(url).reply(200, tableData)

    const wrapper = render(
      <Router>
        <Users />
      </Router>,
    );
    expect(wrapper).toBeTruthy();

    await waitFor(() => {
      tableData.rows.forEach((row) => {
        if (row.avatar === null) {
          const tdElements = screen.getAllByText('/');
          expect(tdElements).toHaveLength(5);
        }
        else {
          const text = screen.getAllByAltText("avatar")
          expect(text).toBeTruthy();
        }
      })
    })
  });
});
