class BluearchAwsGovernance < Formula
  desc "AWS Governance Hub with bundled misconfiguration catalog"
  homepage "https://github.com/bluearchio/bluearch-aws-governance"
  url "https://dist.bluearch.io/releases/bluearch-aws-governance/v0.2.3/cloud-governance-macos-arm64.zip"
  version "v0.2.3"
  sha256 "9ac6a80449f0b32a31e0b0557f3116afaa5b85b1280d4fa048064a2b507adb73"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "cloud-governance"
  end

  def caveats
    <<~EOS
      bluearch-aws-governance has been installed.

      Start BlueArch Core to launch installed dashboards:
        bluearch-core start --daemon
    EOS
  end

  test do
    system "#{bin}/cloud-governance", "--version"
  end
end
