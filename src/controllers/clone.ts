//dependencies
import express, { NextFunction, Request, Response } from 'express';
import shell from 'shelljs';

//declarations
const router = express.Router({ mergeParams: true });
// change your root folder path where you want the repo to be cloned
const path = '/Users/mayankmaurya/resources';

//initializations
shell.cd(path);

router.get('/',async (req: Request, res: Response, next: NextFunction) => {
    try {
        // cloning a easy to parse repo from github
        shell.exec('git clone https://github.com/yicheng-irun/icheng-node-pro-xy.git');
    } catch (err) {
        console.log(err);
        return res.status(500).send('Failed to download repository');
    }
    return res.status(500).send('successfully cloned repository');
});

export default router;