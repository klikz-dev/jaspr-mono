import { ComponentStory } from '@storybook/react';

const DefaultTypography = () => {
    return (
        <div style={{ display: 'flex', flexDirection: 'column' }}>
            <h1>Heading 1</h1>
            <h2>Heading 2</h2>
            <h3>Heading 3</h3>
            <h4>Heading 4</h4>
            <h5>Heading 5</h5>
            <h6>Heading 6</h6>
            <p className="typography--subtitle1">Subtitle 1</p>
            <p className="typography--subtitle2">Subtitle 2</p>
            <p className="typography--body1">Body 1</p>
            <p className="typography--body2">Body 2</p>
            <p className="typography--body3">Body 3</p>
            <p className="typography--button">Button</p>
            <p className="typography--overline">Overline</p>
        </div>
    );
};

export default {
    title: 'Typography/Typography',
    component: DefaultTypography,
};

const Template: ComponentStory<typeof DefaultTypography> = (args) => (
    <DefaultTypography {...args} />
);

export const Typography = Template.bind({});
Typography.args = {};
