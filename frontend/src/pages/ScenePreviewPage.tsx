import React, { useEffect, useState } from "react";
import SceneCard from "../components/SceneCard";
import PlayerControls from "../components/PlayerControls";
import { BASE_URL } from "../api/config";

interface SceneData {
  id: string;
  job_id: string;
  scene_number: number;
  narration: string;
  image_url: string;
}

interface ScenePreviewPageProps {
  jobId: string;
}

const ScenePreviewPage: React.FC<ScenePreviewPageProps> = ({ jobId }) => {
  const [scenes, setScenes] = useState<SceneData[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    const fetchScenes = async () => {
      try {
        const res = await fetch(`${BASE_URL}/scenes/by_job/${jobId}`);
        if (!res.ok) throw new Error("Failed to fetch scenes");
        const data = await res.json();
        setScenes(data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchScenes();
  }, [jobId]);

  useEffect(() => {
    let timer: number;
    if (isPlaying && scenes.length > 0) {
      timer = window.setTimeout(() => {
        if (currentIndex < scenes.length - 1) setCurrentIndex(currentIndex + 1);
        else setIsPlaying(false);
      }, 5000);
    }
    return () => clearTimeout(timer);
  }, [isPlaying, currentIndex, scenes.length]);

  if (!scenes.length) return <div className="p-4 text-center">Loading scenes...</div>;

  const currentScene = scenes[currentIndex];

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Scene {currentScene.scene_number}</h1>
      <SceneCard
        sceneId={currentScene.scene_number}
        imageUrl={
          currentScene.image_url?.startsWith("data:")
            ? currentScene.image_url
            : currentScene.image_url
            ? `${BASE_URL}${currentScene.image_url}`
            : ""
        }
        narrationText={currentScene.narration}
      />
      <PlayerControls
        currentScene={currentIndex + 1}
        totalScenes={scenes.length}
        onNext={() => setCurrentIndex(Math.min(currentIndex + 1, scenes.length - 1))}
        onPrevious={() => setCurrentIndex(Math.max(currentIndex - 1, 0))}
        onPlayAll={() => setIsPlaying(!isPlaying)}
        isPlaying={isPlaying}
      />
    </div>
  );
};

export default ScenePreviewPage;
