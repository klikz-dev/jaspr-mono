import { useState } from 'react';

interface RenderProps {
    editMode: boolean;
    toggleEditMode: () => void;
}

interface Props {
    render: (props: RenderProps) => JSX.Element;
}

const EditModeArea = (props: Props) => {
    const { render } = props;
    const [editMode, setEditMode] = useState(false);
    const toggleEditMode = () => setEditMode(!editMode);
    return render({ editMode, toggleEditMode });
};

export default EditModeArea;
