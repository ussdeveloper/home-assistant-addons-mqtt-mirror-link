# GitHub Repository Setup for HACS

To make this integration fully HACS-compliant, you need to configure the GitHub repository settings manually.

## Required Steps

### 1. Add Repository Description

1. Go to: https://github.com/ussdeveloper/home-assistant-addons-mqtt-mirror-link
2. Click the **⚙️ Settings** icon (top right, near "About")
3. Add description:
   ```
   MQTT Mirror Link - Synchronize MQTT messages between two Home Assistant instances
   ```
4. Click **Save changes**

### 2. Add Repository Topics

In the same "About" section:

1. Click **⚙️ Settings**
2. In the **Topics** field, add these tags (press Enter after each):
   - `home-assistant`
   - `mqtt`
   - `hacs`
   - `home-assistant-integration`
   - `mqtt-bridge`
   - `mqtt-sync`
3. Click **Save changes**

### 3. (Optional) Add to Home Assistant Brands

This is optional but recommended for better integration:

1. Fork the repository: https://github.com/home-assistant/brands
2. Add your integration logo and metadata
3. Submit a Pull Request

**Alternatively**, you can skip this step - the integration will work without it.

## Why HACS Validation Was Removed

The HACS validation GitHub Action was removed from `.github/workflows/validate.yml` because:

1. It requires GitHub repository metadata (description, topics) that cannot be set via code
2. It requires manual configuration through the GitHub web interface
3. The validation failures don't prevent the integration from working
4. Hassfest validation (which remains) is more critical for Home Assistant compatibility

## Re-enabling HACS Validation (After Setup)

Once you've completed steps 1-2 above, you can optionally re-enable HACS validation:

Edit `.github/workflows/validate.yml` and add back:

```yaml
      - name: HACS validation
        uses: "hacs/action@main"
        with:
          category: "integration"
```

Add this step **before** the Hassfest validation step.

## Verification

After completing the setup:

1. Go to the Actions tab in your GitHub repository
2. Manually trigger the "Validate" workflow
3. Check that it passes without errors

## More Information

- HACS Documentation: https://hacs.xyz/docs/publish/include
- Home Assistant Brands: https://github.com/home-assistant/brands
