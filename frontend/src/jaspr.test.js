import React from 'react';
import ReactDOM from 'react-dom';
import Jaspr from './jaspr';

it('renders without crashing', () => {
    const div = document.createElement('div');
    ReactDOM.render(<Jaspr />, div);
    ReactDOM.unmountComponentAtNode(div);
});
