declare module '*.scss' {
    const content: { [className: string]: string };
    export = content;
}

declare module '*.jpg';

declare module '*.gif';
declare module '*.png' {
    const value: any;
    export = value;
}

declare module '*.mp4' {
    const content: any;
    export default content;
}

declare module '*.svg' {
    //const content: React.FunctionComponent<React.SVGAttributes<SVGElement>>;
    const content: any;
    export default content;
}
