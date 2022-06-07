import { css } from 'styled-components';

const button = css`
    display: flex;
    flex-shrink: 0;
    margin: 10px 0;
    padding: 0 45px;
    height: 58px;
    width: auto;
    border-radius: 4px;
    border-style: solid;
    justify-content: center;
    align-items: center;
    max-width: 388px;
`;

const web = css`
    cursor: pointer;
    user-select: none;
    transition: 1s ease;
`;

const primary = css`
    border-color: rgba(0, 157, 180, 1);
    background-color: rgba(0, 157, 180, 1);
`;

const secondary = css`
    border-color: rgba(0, 157, 180, 1);
    background-color: rgba(255, 255, 255, 1);
`;

const disabled = css`
    background-color: rgba(170, 173, 183, 1);
    border-color: rgba(170, 173, 183, 1);
`;

const text = css`
    font-size: 17px;
    line-height: 20px;
    color: ${({ theme }) => theme.color};
    font-weight: ${({ theme }) => theme.fontWeight};
`;

/* eslint import/no-anonymous-default-export: [2, {"allowObject": true}] */
export default {
    button,
    primary,
    secondary,
    web,
    text,
    disabled,
};
