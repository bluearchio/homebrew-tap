class BluearchAwsGovernance < Formula
  desc "AWS Governance Hub with bundled misconfiguration catalog"
  homepage "https://github.com/bluearchio/bluearch-aws-governance"
  url "https://github.com/bluearchio/bluearch-aws-governance/releases/download/v0.2.5/bluearch-aws-governance-macos-arm64.zip"
  version "0.2.5"
  sha256 "bf0db49fc3ac46400d5f7d2484f2505553d0744ed6cf92eb5c77e2477211aff7"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "bluearch-aws-governance"
  end

  def caveats
    <<~EOS
      bluearch-aws-governance has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-governance --help

      Load the bundled catalog:
        bluearch-aws-governance catalog import
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-governance", "--version"
  end
end
