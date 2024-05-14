import { Button } from "react-bootstrap";
import { useNotification } from "../../notification/NotificationContext";

const TestButton = ({message, variant}) => {
    const showNotification = useNotification();

    return (
        <Button 
            variant="primary"
            onClick={() => showNotification(message, variant)}
        >Test Button</Button>
    );
}

export default TestButton;