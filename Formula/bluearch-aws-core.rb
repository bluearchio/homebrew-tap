class BluearchAwsCore < Formula
  desc "Shared local runtime for BlueArch AWS tools"
  homepage "https://github.com/bluearchio/bluearch-aws-core"
  url "https://github.com/bluearchio/bluearch-aws-core/releases/download/v0.2.9/bluearch-aws-core-macos-arm64.zip"
  version "0.2.9"
  sha256 "6da8ea8d6033cd5fd018fdacd89041c4ef30877cd31ab36bc5c68a381a2b5855"
  license "MIT"

  depends_on arch: :arm64

  def install
    bin.install "bluearch-aws-core"
  end

  def caveats
    <<~EOS
      bluearch-aws-core has been installed.

      Commands:
        bluearch-aws-core --help

      Start the shared runtime before using the other BlueArch AWS tools:
        bluearch-aws-core start --daemon

      API docs:
        http://127.0.0.1:8094/docs
    EOS
  end

  test do
    system "#{bin}/bluearch-aws-core", "--version"
  end
end
