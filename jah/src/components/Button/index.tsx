import React from 'react';
import View from './button';

type Props = {
    label: string;
    secondary?: boolean;
    style?: React.CSSProperties;
    theme?: React.CSSProperties;
    disabled?: boolean;
} & (
    | {
          onClick?: (e: any) => void;
          submit?: undefined;
      }
    | {
          submit?: (e: React.FormEvent<HTMLFormElement>) => void;
          onClick?: undefined;
      }
);

export type ViewProps = Props & { theme: React.CSSProperties };

const Button = ({ style, submit, label, onClick, secondary = false, disabled = false }: Props) => {
    const fontWeight = secondary ? ('inherit' as const) : 600;
    const theme = {
        fontWeight: fontWeight,
        color: secondary ? 'rgba(23, 155, 176, 1)' : 'rgba(255, 255, 255, 1)',
    };

    return (
        <>
            {/* @ts-ignore */}
            <View
                submit={submit}
                secondary={secondary}
                onClick={onClick}
                style={style}
                label={label}
                theme={theme}
                disabled={disabled}
            />
        </>
    );
};

export default Button;
