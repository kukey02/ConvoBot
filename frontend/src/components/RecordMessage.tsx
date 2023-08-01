import { ReactMediaRecorder } from "react-media-recorder";
import RecordIcon from "./RecordIcon";

type Props = {
  handleStop: any;
};

const RecordMessage = ({ handleStop }: Props) => {
  return (
    <ReactMediaRecorder
      audio
      onStop={handleStop}
      render={({ status, startRecording, stopRecording }) => (
        <div className="mt-2">
          <button
            onMouseDown={startRecording}
            onMouseUp={stopRecording}
            className=" bg-gradient-to-b from-gray-900 to-gray-500  p-4 rounded-full animate-bounce "
          >
            <RecordIcon
              classText={
                status == "recording"
                  ? "animate-spin text-green-500 "
                  : "text-sky-400"
              }
            />
          </button>
          <p className="mt-2 text-black font-light">{status}</p>
        </div>
      )}
    />
  );
};

export default RecordMessage;