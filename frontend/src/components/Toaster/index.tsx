import { Toaster as ToasterComponent } from 'react-hot-toast';

const Toaster = () => {
    return (
        <ToasterComponent
            position="bottom-center"
            toastOptions={{
                className: 'jaspr-toast',
                icon: null,
                custom: {
                    duration: 6000,
                },
            }}
        />
    );
};

export default Toaster;
