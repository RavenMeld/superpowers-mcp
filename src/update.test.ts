import { describe, it, expect, vi, beforeEach } from 'vitest';
import { checkAndApplyUpdates, isAutoUpdateEnabled } from './update.js';
import * as config from './config.js';
import * as git from './git.js';
import * as fs from 'node:fs';

vi.mock('./config.js');
vi.mock('./git.js');
vi.mock('node:fs');

describe('checkAndApplyUpdates', () => {
    const enabledEnv = { SUPERPOWERS_ENABLE_AUTO_UPDATE: '1' } as NodeJS.ProcessEnv;

    beforeEach(() => {
        vi.clearAllMocks();
        (fs.existsSync as any).mockReturnValue(true);
    });

    it('should do nothing when auto-update is disabled', async () => {
        await checkAndApplyUpdates({ env: {} as NodeJS.ProcessEnv });
        expect(git.checkForUpdates).not.toHaveBeenCalled();
    });

    it('should do nothing if no skills dir', async () => {
        (config.getSkillsDir as any).mockReturnValue(undefined);
        await checkAndApplyUpdates({ env: enabledEnv });
        expect(git.checkForUpdates).not.toHaveBeenCalled();
    });

    it('should do nothing if not enough time passed', async () => {
        (config.getSkillsDir as any).mockReturnValue('/tmp/skills');
        (config.getLastUpdateCheck as any).mockReturnValue(Date.now()); // check just happened
        await checkAndApplyUpdates({ env: enabledEnv });
        expect(git.checkForUpdates).not.toHaveBeenCalled();
    });

    it('should check for updates if time passed', async () => {
        (config.getSkillsDir as any).mockReturnValue('/tmp/skills');
        (config.getLastUpdateCheck as any).mockReturnValue(Date.now() - (25 * 60 * 60 * 1000)); // 25 hours ago
        (git.checkForUpdates as any).mockResolvedValue(false);

        await checkAndApplyUpdates({ env: enabledEnv });
        expect(git.checkForUpdates).toHaveBeenCalledWith('/tmp/skills');
        expect(git.gitPull).not.toHaveBeenCalled();
        expect(config.setLastUpdateCheck).toHaveBeenCalled();
    });

    it('should pull updates if available', async () => {
        (config.getSkillsDir as any).mockReturnValue('/tmp/skills');
        (config.getLastUpdateCheck as any).mockReturnValue(0);
        (git.checkForUpdates as any).mockResolvedValue(true);

        await checkAndApplyUpdates({ env: enabledEnv });
        expect(git.gitPull).toHaveBeenCalledWith('/tmp/skills');
        expect(config.setLastUpdateCheck).toHaveBeenCalled();
    });

    it('should handle errors gracefully', async () => {
        (config.getSkillsDir as any).mockReturnValue('/tmp/skills');
        (config.getLastUpdateCheck as any).mockReturnValue(0);
        (git.checkForUpdates as any).mockRejectedValue(new Error('git failed'));

        // Should not throw
        await checkAndApplyUpdates({ env: enabledEnv });
    });
});

describe('isAutoUpdateEnabled', () => {
    it('accepts common truthy values', () => {
        expect(isAutoUpdateEnabled({ SUPERPOWERS_ENABLE_AUTO_UPDATE: '1' } as NodeJS.ProcessEnv)).toBe(true);
        expect(isAutoUpdateEnabled({ SUPERPOWERS_ENABLE_AUTO_UPDATE: 'true' } as NodeJS.ProcessEnv)).toBe(true);
        expect(isAutoUpdateEnabled({ SUPERPOWERS_ENABLE_AUTO_UPDATE: 'yes' } as NodeJS.ProcessEnv)).toBe(true);
    });

    it('defaults to false when missing', () => {
        expect(isAutoUpdateEnabled({} as NodeJS.ProcessEnv)).toBe(false);
    });
});
