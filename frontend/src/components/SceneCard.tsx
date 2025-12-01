import React from "react";

interface SceneCardProps {
  sceneId: number;
  imageUrl: string;
  narrationText: string;
  onRegenerate?: (sceneId: number) => void;
}

const SceneCard: React.FC<SceneCardProps> = ({
  sceneId,
  imageUrl,
  narrationText,
  onRegenerate,
}) => {
  return (
    <div className="scene-card border rounded-lg shadow-lg p-4 m-2 bg-white">
      <h3 className="text-lg font-bold mb-2">Scene {sceneId}</h3>
      <img
        src={imageUrl || `https://placehold.co/800x450?text=Scene+${sceneId}`}
        alt={`Scene ${sceneId}`}
        className="w-full h-64 object-cover rounded-md mb-2"
      />
      <p className="text-gray-700 mb-2">{narrationText}</p>
      {onRegenerate && (
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={() => onRegenerate(sceneId)}
        >
          Regenerate Scene
        </button>
      )}
    </div>
  );
};

export default SceneCard;
