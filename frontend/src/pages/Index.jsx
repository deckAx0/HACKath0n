import {useState} from "react"
import BinFileDrop from "../components/FileDropzone"

export default function Index() {
	const [file, setFile] = useState(null)

	const handleUpload = async () => {
		if(!file) return;
		const formData = new FormData();
		formData.append('file', file);

		await fetch('/api/upload', {
			method: 'POST',
			body: formData,
		})
	}

	return (
		<>
			<h1>Головна</h1>
			<BinFileDrop onFileSelected={setFile} />
			{file && (
				<div className="mt-2">
					<p>Обрано: {file.name}</p>
					<button onClick={handleUpload}>Візуалізувати</button>
				</div>
			)}
		</>
	)
}
