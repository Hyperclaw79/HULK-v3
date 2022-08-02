/** The component which holds the status of the Target website. */

import Status, { statusLevelMap } from "./status";
import { TargetProps } from "../../types/props.d";


const Target = (props: TargetProps) => {
    return (
        <div className="targetContainer">
            <div className="target">
                <a href={props.url} className="targetUrl">
                    {
                        props.url ? (
                            <>
                                Attacking&nbsp;
                                <span>{props.url}</span>
                            </>
                        ) : (
                            'Waiting for target...'
                        )
                    }
                </a>
                <div className="targetStatus">
                    Status:&nbsp;
                    <div className="statusWrapper">
                        <Status
                            status={
                                // Remove the StatusCodes. prefix from the status.
                                (props.status || 'UNKNOWN')
                                .replace(/StatusCodes\./, '')
                                .replace(/_/, ' ')
                            }
                            level={statusLevelMap[props.status]}
                        />
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Target;
