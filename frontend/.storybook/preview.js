import { action } from '@storybook/addon-actions';
import Modal from 'react-modal';
import { MemoryRouter } from 'react-router';
import { withReactContext } from 'storybook-react-context';
import Store from 'state/store';
import rootReducer from 'state/reducers';
import StoreContext from 'state/context/store';
import { initialState } from 'state/reducers';

window.analytics = {
    track: action('analytics Track'),
    reset: action('Analytics Reset'),
};

import '../src/index.scss';
export const parameters = {
    actions: { argTypesRegex: '^on[A-Z].*' },
    controls: {
        matchers: {
            color: /(background|color)$/i,
            date: /Date$/,
        },
    },
    backgrounds: {
        default: 'light',
        values: [
            {
                name: 'light',
                value: '#fff',
            },
            {},
            {
                name: 'dark',
                value: 'rgba(52, 50, 69, 1)',
            },
        ],
    },
};

export const decorators = [
    withReactContext({ context: StoreContext, reducer: rootReducer, initialState }),
    (Story) => {
        Modal.setAppElement('#root');
        return (
            <MemoryRouter initialEntries={['/']}>
                <Story />
            </MemoryRouter>
        );
    },
];
