import { ReactChild } from 'react';
import CSS from 'csstype';

import styles from './index.module.scss';
import Plus from 'assets/icons/Plus';
import Copy from 'assets/icons/Copy';
import Upload from 'assets/icons/Upload';
import QuestioMarkCircle from 'assets/icons/QuestionMarkCircle';

type icon = 'upload' | 'plus' | 'copy' | 'help';
export type ButtonProps = {
    variant?: 'primary' | 'secondary' | 'tertiary';
    disabled?: boolean;
    icon?: icon;
    dark?: boolean;
    name?: string;
    style?: CSS.Properties;
    children?: ReactChild | ReactChild[];
} & (
    | {
          type?: 'button' | 'reset';
          onClick?: (
              e: React.MouseEvent<HTMLButtonElement> | React.TouchEvent<HTMLButtonElement>,
          ) => void;
      }
    | {
          type?: 'submit';
          onClick?: undefined;
      }
);

const Button = ({
    type = 'button',
    disabled = false,
    variant = 'primary',
    icon,
    dark = false,
    name,
    onClick,
    style = {},
    children,
}: ButtonProps) => {
    const getIconColor = () => {
        if (variant === 'primary' && dark && !disabled) {
            return 'rgba(255, 255, 255, 1)';
        } else if (variant === 'primary' && !dark) {
            return 'rgba(0, 0, 0, 1)';
        } else if (variant === 'primary' && disabled) {
            return 'rgba(71, 71, 71, 1)';
        } else if (variant === 'secondary' && dark) {
            return 'rgba(255, 255, 255, 1)';
        } else if (variant === 'secondary' && !dark) {
            return 'rgba(0, 0, 0, 1)';
        } else if (variant === 'tertiary' && dark && !disabled) {
            return 'rgba(124, 223, 255, 1)';
        } else if (variant === 'tertiary' && !dark && !disabled) {
            return 'rgba(17, 115, 131, 1)';
        } else if (variant === 'tertiary' && dark && disabled) {
            return 'rgba(127, 127, 127, 1)';
        } else if (variant === 'tertiary' && !dark && disabled) {
            return 'rgba(184, 188, 204, 1)';
        }
        return 'rgba(255, 255, 255, 1)';
    };

    const getIcon = (icon: icon) => {
        const props = {
            color: getIconColor(),
            ariaHidden: true,
            height: 18,
        };
        switch (icon) {
            case 'upload':
                return <Upload {...props} />;
            case 'plus':
                return <Plus {...props} />;
            case 'copy':
                return <Copy {...props} />;
            case 'help':
                return <QuestioMarkCircle {...props} />;
            default:
                return null;
        }
    };

    return (
        <button
            type={type}
            className={`${styles.button} ${styles[variant]} ${dark ? styles.dark : ''}`}
            disabled={disabled}
            name={name}
            style={style}
            onClick={onClick}
        >
            {getIcon(icon)}
            {children}
        </button>
    );
};
export { Button };
export default Button;
