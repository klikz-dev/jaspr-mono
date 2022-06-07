import { useEffect } from 'react';
import MockAdapter from 'axios-mock-adapter';
import axios from 'axios';

interface IProps {
    children: any;
    mock: (adapter: MockAdapter) => void;
}

const apiMock = new MockAdapter(axios);

const AxiosMock = ({ children, mock }: IProps) => {
    useEffect(() => {
        mock(apiMock);
        return () => {
            apiMock.reset();
        };
    });
    return children;
};

export default AxiosMock;
