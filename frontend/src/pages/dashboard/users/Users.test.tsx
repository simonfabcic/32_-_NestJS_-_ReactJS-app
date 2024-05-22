import { describe, test, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import { BrowserRouter as Router } from "react-router-dom";
import MockAdapter from "axios-mock-adapter";
import axios from "axios";

import Users from "./Users";

const mock = new MockAdapter(axios, { onNoMatch: "throwException" });

const tableData = {
  headers: [
    {key: 'avatar', label: 'Avatar', sorting: false},
    {key: 'email', label: 'Email', sorting: false},
    {key: 'full_name', label: 'Full name', sorting: true},
    {key: 'role', label: 'Role', sorting: true},
  ],
  pagination_description: {
    current_page: 1,
    next_page: null,
    page_size: 100,
    prev_page: null,
    sort_by: "role",
    sort_order: "ASC",
    total_pages: 1,
    total_records: 98
  },
  rows: [
    {
      avatar: "/media/images/avatars/download_1.jpg",
      email: "emma.martin@email.com",
      first_name: "Emma",
      full_name: "Emma Martin",
      id: 2,
      last_name: "Martin",
      role: "Administrator",
      username: "emma.martin@email.com"
    },
    {
      avatar: null,
      email: "alexander.jackson@email.com",
      first_name: "Alexander",
      full_name: "Alexander Jackson",
      id: 18,
      last_name: "Jackson",
      role: "Administrator",
      username: "alexander.jackson@email.com"
    },
    {
      avatar: null,
      email: "jane.thompson@email.com",
      first_name: "Jane",
      full_name: "Jane Thompson",
      id: 22,
      last_name: "Thompson",
      role: "Administrator",
      username: "jane.thompson@email.com"
    },
    {
      avatar: null,
      email: "elijah.jones@email.com",
      first_name: "Elijah",
      full_name: "Elijah Jones",
      id: 25,
      last_name: "Jones",
      role: "Administrator",
      username: "elijah.jones@email.com"
    },
    {
      avatar: null,
      email: "abigail.white@email.com",
      first_name: "Abigail",
      full_name: "Abigail White",
      id: 26,
      last_name: "White",
      role: "Administrator",
      username: "abigail.white@email.com"
    },
    {
      avatar: null,
      email: "amelia.lewis@email.com",
      first_name: "Amelia",
      full_name: "Amelia Lewis",
      id: 28,
      last_name: "Lewis",
      role: "Administrator",
      username: "amelia.lewis@email.com"
    }
  ]
}

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
});