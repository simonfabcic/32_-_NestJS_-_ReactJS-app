import { describe, test, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import Users from './Users'
import { BrowserRouter as Router } from "react-router-dom";

describe('<App />', () => {
    test('App mounts properly', () => {
        const wrapper = render(
            <Router>
                <Users />
            </Router>
        )
        expect(wrapper).toBeTruthy()
        
        const text = screen.getByText(
        /Users/i
        );
        expect(text.textContent).toBeTruthy()

        const b1 = wrapper.container.querySelector('button')
        expect(b1?.textContent).toBe('Add User')
    })
});