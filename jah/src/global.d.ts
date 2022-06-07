declare module '*.scss' {
    const content: { [className: string]: string };
    export = content;
}

declare module '*.css' {
    const content: { [className: string]: string };
    export = content;
}

declare module 'subtitles-parser-vtt';

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

// Add browser to process property.  'browser' is added by Webpack and is not universal.
// We use process.browser in sharedStories.
// See https://github.com/vercel/next.js/issues/2177
declare namespace NodeJS {
    interface Process {
        browser: boolean;
    }
}
