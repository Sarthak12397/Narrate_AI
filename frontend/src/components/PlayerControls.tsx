import React from "react";

interface PlayerControlsProps {
  currentScene: number;
  totalScenes: number;
  onNext: () => void;
  onPrevious: () => void;
  onPlayAll: () => void;
  isPlaying: boolean;
}

const PlayerControls: React.FC<PlayerControlsProps> = ({
  currentScene,
  totalScenes,
  onNext,
  onPrevious,
  onPlayAll,
  isPlaying,
}) => {
  return (
    <div className="player-controls flex items-center space-x-4 mt-4">
      <button
        className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
        onClick={onPrevious}
        disabled={currentScene === 1}
      >
        Previous
      </button>

      <button
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
        onClick={onPlayAll}
      >
        {isPlaying ? "Pause" : "Play All"}
      </button>

      <button
        className="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
        onClick={onNext}
        disabled={currentScene === totalScenes}
      >
        Next
      </button>

      <span className="text-sm text-gray-600">
        Scene {currentScene} / {totalScenes}
      </span>
    </div>
  );
};

export default PlayerControls;
