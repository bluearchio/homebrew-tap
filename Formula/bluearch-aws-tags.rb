class BluearchAwsTags < Formula
  desc "AWS tagging, lifecycle, tag policy, and FinOps CLI"
  homepage "https://github.com/bluearchio/bluearch-aws-tags"
  url "https://github.com/bluearchio/bluearch-aws-tags/releases/download/v0.12.5/bluearch-aws-tags-macos-arm64.zip"
  version "0.12.5"
  sha256 "434b1fc0286e09745e66fd85a5a6237b606be7a86ac3a5aa6068b9cd5f1e6c6a"
  license "MIT"

  depends_on arch: :arm64
  depends_on "bluearch-aws-core"

  def install
    bin.install "bluearch-aws-tags"
  end

  def caveats
    <<~EOS
      bluearch-aws-tags has been installed.

      Start Core first:
        bluearch-aws-core start --daemon

      Commands:
        bluearch-aws-tags --help

      Getting started:
        bluearch-aws-tags setup validate

      Configure AWS credentials:
        export AWS_PROFILE=your-profile
        aws sso login

      Data is stored locally by the product runtime.
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-tags", "--version"
  end
end
