import { createBrowserRouter } from 'react-router-dom';
import Index from '../pages/Index';
import NotFound from '../pages/NotFound';

const router = createBrowserRouter([
	{
		path: "/",
		element: <Index />
	},
	{
		path: "*",
		element: <NotFound />
	}
])

export default router;
