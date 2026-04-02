import {useCallback} from "react";
import { useDropzone } from "react-dropzone";

function BinFileDrop({ onFileSelected }) {
	const { getRootProps, getInputProps, isDragActive, fileRejections } = useDropzone({
		onDrop: useCallback((acceptedFiles) => {
			if(acceptedFiles.length > 0) {
				onFileSelected(acceptedFiles[0]);
			}
		}, [onFileSelected]),
		multiple: false,
		maxSize: 10*1024*1024,
		accept: {
			"application/octet-stream": [".bin"],
		},
	})
	
	return (
		<div {...getRootProps()} className="border-2 border-dashed border-gray-400 p-8 text-center cursor-pointer">
			<input {...getInputProps()} />
			{ isDragActive ? (
				<p>Відпустіть файл</p>
			) : (
				<p>Перетягніть і відпустіть .bin файл (до 10 МБ), або натисніть щоб вибрати.</p>
			)}

			{fileRejections.length > 0 && (
				<ul className="text-red-600 mt-2">
					{fileRejections.map(({file, errors}) => (
						<li key={file.path}>
							{file.path} - {file.size/1024/1024} МБ
							<ul>
								{errors.map((e) => (
									<li key={e.code}>{e.message}</li>
								))}
							</ul>
						</li>
					))}
				</ul>
			)}
		</div>
	)
}

export default BinFileDrop
