import React from 'react';
import ReactDOM from 'react-dom';
import ccEnabled from 'assets/cc-toggled.svg';
import ccDisabled from 'assets/cc-untoggled.svg';

interface CCButtonProps {
    ccButtonNodeRef: React.RefObject<HTMLDivElement>;
    captionState: boolean;
    setCaptionState: (state: (enable: boolean) => boolean) => void;
}

const CCButton = ({ ccButtonNodeRef, captionState, setCaptionState }: CCButtonProps) => {
    const Button = (
        <img
            src={captionState ? ccEnabled : ccDisabled}
            style={
                ccButtonNodeRef?.current
                    ? {}
                    : {
                          position: 'absolute',
                          bottom: '-61px',
                          right: '28px',
                          cursor: 'point',
                      }
            }
            onClick={() => {
                setCaptionState((currentState) => !currentState);
            }}
            alt={captionState ? 'Turn captions off' : 'Turn captions on'}
        />
    );

    if (ccButtonNodeRef?.current) {
        return ReactDOM.createPortal(Button, ccButtonNodeRef.current);
    }

    return Button;
};

export default CCButton;
