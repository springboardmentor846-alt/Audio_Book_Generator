export default function AudioPlayer({ audioUrl }) {
  if (!audioUrl) {
    return <p className="text-gray-400">No audio generated</p>;
  }

  return (
    <div className="bg-black/30 p-4 rounded-xl">
      <audio controls src={audioUrl} className="w-full" />
    </div>
  );
}